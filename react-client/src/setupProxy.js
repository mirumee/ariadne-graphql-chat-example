const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/ws",
    createProxyMiddleware("/ws", {
      target: "ws://localhost:3000",
      ws: true,
    })
  );
  app.use(
    "/graphql",
    createProxyMiddleware("/graphql", {
      target: "http://localhost:8000",
      changeOrigin: true,
      ws: true,
    })
  );
};
