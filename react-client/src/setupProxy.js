const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  // Proxy dev-server requests
  app.use(
    "/ws",
    createProxyMiddleware("/ws", {
      target: "ws://localhost:3000",
      ws: true,
    })
  );
  // Proxy client's GraphQL requests
  app.use(
    "/graphql",
    createProxyMiddleware("/graphql", {
      target: "http://localhost:8000",
      changeOrigin: true,
      ws: true, // Support websockets
    })
  );
};
