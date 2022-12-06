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
COLOR = [
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
shuffle(COLOR)


def time_now():
    return datetime.now().isoformat()


def str_to_color(src_str):
    str_hash = md5((src_str * 5).encode("utf-8")).hexdigest()
    hash_values = (str_hash[:8], str_hash[8:16], str_hash[16:24])
    color_index = sum(int(value, 16) % 256 for value in hash_values) % len(COLOR)
    return COLOR[color_index]


pubsub = Broadcast("redis://redis:6379")
history = [
    {
        "sender": "System",
        "color": "#64748b",
        "message": f"Chat started",
        "timestamp": time_now(),
    },
]

type_defs = load_schema_from_path("schema.graphql")


query = QueryType()


@query.field("history")
def resolve_history(*_):
    return history[-10:]  # Last 10 messages


mutation = MutationType()


@mutation.field("reply")
async def resolve_reply(*_, **message):
    message["color"] = str_to_color(message["sender"])
    message["timestamp"] = time_now()
    history.append(message)
    await pubsub.publish(channel="chatroom", message=json.dumps(message))
    return True


subscription = SubscriptionType()


@subscription.source("message")
async def source_message(_, info):
    async with pubsub.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            yield json.loads(event.message)


@subscription.field("message")
def resolve_message(event, info):
    return event


schema = make_executable_schema(type_defs, query, mutation, subscription)
graphql = GraphQL(
    schema=schema,
    debug=True,
    websocket_handler=GraphQLTransportWSHandler(),
)

app = Starlette(
    debug=True,
    on_startup=[pubsub.connect],
    on_shutdown=[pubsub.disconnect],
)

app.mount("/graphql/", graphql)
app.add_websocket_route("/graphql/", graphql)
