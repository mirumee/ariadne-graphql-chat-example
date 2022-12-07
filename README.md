# Ariadne GraphQL Chat Example

This repo contains an example of simple chat application demoing GraphQL subscriptions feature in Ariadne.

It has following Python dependencies:

- Ariadne: GraphQL server
- Starlette: ASGI application, WebSocket route
- Uvicorn: ASGI and WebSocket app server
- Broadcaster: Messaging between chat clients

Server uses Redis for messaging.

Example client was implemented with:

- create-react-app: Project setup and dev tools
- React 18: UI library
- Apollo-Client 3.7: GraphQL client
- GraphQL-WS 5.11: GraphQL WebSockets protocol


## Demo

Chat in action:

![Demo](https://user-images.githubusercontent.com/750553/205963257-39d062a8-34d5-4f65-b8a5-608aee5c2a46.gif)


## Installation

Clone repo on your computer:

```
git clone git@github.com:mirumee/ariadne-graphql-chat-example.git
```

In cloned directory build Python chat and Redis services using Docker Compose:

```
docker-compose build
```

Move to `react-client` directory and install client's dependencies:

```
npm install 
```


## Running

Run following command in cloned directory to start Docker Compose services:

```
docker-compose up
```

If you get an error about bind for 0.0.0.0:8000 failing, check if there's nothing else running on port 8000.

GraphQL explorer can be found under the http://localhost:8000/graphql/ address.

To start client, move to `react-client` directory and run following:

```
npm run start
```

Open a web browser of your liking and navigate to http://localhost:3000/ start chatting. Every browser tab will be separate chat session, so you can open as many as you like to experiment with multiple users.

> **Note:** sometimes `http-proxy-middleware` used by the dev server to proxy requests to the GraphQL acts funky about proxying websockets and there's a delay between dev server starting and accepting websocket connections. This results in `upgrade: websocket` requests for `/graphql` stalling in the browser. This issue usually resolves itself after refresh or few.


## Contributing

If you've found a bug with this repo or want to contribute an improvement, feel free to open an issue or pull request!

Also make sure you follow [@AriadneGraphQL](https://twitter.com/AriadneGraphQL) on Twitter for latest updates, news and random musings!

**Crafted with ❤️ by [Mirumee Software](http://mirumee.com)**
hello@mirumee.com
