import json
from datetime import datetime
from random import shuffle
from hashlib import md5

from ariadne import (
    MutationType,
    QueryType,
    SubscriptionType,
    load_schema_from_path,
    make_executable_schema,
) 
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from broadcaster import Broadcast
from starlette.applications import Starlette

# Tailwind Color Palette 600's
COLORS = [
    "#dc2626",
    "#ea580c",
    "#d97706",
    "#ca8a04",
    "#65a30d",
    "#16a34a",
    "#059669",
    "#0d9488",
    "#0891b2",
    "#0284c7",
    "#2563eb",
    "#4f46e5",
    "#7c3aed",
    "#9333ea",
    "#c026d3",
    "#db2777",
    "#e11d48",
]
shuffle(COLORS)


def time_now():
    return datetime.now().isoformat()


def str_to_color(src_str):
    # Returns unique color for given string
    str_hash = md5((src_str * 5).encode("utf-8")).hexdigest()
    hash_values = (str_hash[:8], str_hash[8:16], str_hash[16:24])
    color_index = sum(int(value, 16) % 256 for value in hash_values) % len(COLORS)
    return COLORS[color_index]


# Setup broadcaster to use Redis as messaging backend
pubsub = Broadcast("redis://redis:6379")

# Simple messages history
history = [
    {
        "sender": "System",
        "color": "#64748b",
        "message": f"Chat started",
        "timestamp": time_now(),
    },
]

# Load schema from file
type_defs = load_schema_from_path("schema.graphql")


# Query type with single field returning last 10 messages
query = QueryType()


@query.field("history")
def resolve_history(*_):
    return history[-10:]  # Last 10 messages


# Mutation type with single mutation that sends chat message to broadcaster
mutation = MutationType()


@mutation.field("reply")
async def resolve_reply(*_, **message):
    # Complete message with color and timestamp
    message["color"] = str_to_color(message["sender"])
    message["timestamp"] = time_now()

    # Append message to history
    history.append(message)

    # Broadcast message to subscribers
    await pubsub.publish(channel="chatroom", message=json.dumps(message))

    return True


# Subscription type that sends new messages to clients
subscription = SubscriptionType()


@subscription.source("message")
async def source_message(_, info):
    # Source consumes events from message source and sends them to resolvers
    # It can also implement filtering logic and skip messages via 'continue'
    async with pubsub.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            message = json.loads(event.message)
            if "politics" in message["message"].lower():
                continue

            yield message


@subscription.field("message")
def resolve_message(event, info):
    # 'event' passed to resolver is result of source function
    # Depending on implementation it can be final message to send to clients
    # or just the data that can be used to construct final message, eg.
    # ID of item that was updated by other user that should be pulled from
    # the database in resolver and then returned to clients
    return event


# Create executable schema and ASGI GraphQL application that supports websockets
schema = make_executable_schema(type_defs, query, mutation, subscription)
graphql = GraphQL(
    schema=schema,
    debug=True,
    websocket_handler=GraphQLTransportWSHandler(),
)

# Setup Starlette ASGI app with events to start and stop Broadcaster 
app = Starlette(
    debug=True,
    on_startup=[pubsub.connect],
    on_shutdown=[pubsub.disconnect],
)

# Mount ASGI app to handle GET and POST methods
app.mount("/graphql/", graphql)

# Mount ASGI app to handle websocket connections
app.add_websocket_route("/graphql/", graphql)
