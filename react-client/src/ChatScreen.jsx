import * as React from "react";
import useHistoryQuery from "./useHistoryQuery";
import useMessageSubscription from "./useMessageSubscription";
import useReplyMutation from "./useReplyMutation";

function ChatScreen({ username }) {
  const [messages, setMessages] = React.useState([]);
  const [reply, setReply] = React.useState("");

  const [sendReply] = useReplyMutation();
  const { data } = useHistoryQuery();

  React.useEffect(() => {
    if (data) setMessages(data.history);
  }, [data]);

  useMessageSubscription(({ data }) => {
    setMessages((state) => {
      return [...state, data.data.message];
    });
  });

  return (
    <form
      className="chat-screen"
      onSubmit={(ev) => {
        const cleanReply = reply.trim();
        if (cleanReply.length) {
          setReply("");
          try {
            sendReply({
              variables: { sender: username, message: reply },
            });
          } catch (error) {}
        }

        ev.preventDefault();
        return false;
      }}
    >
      <div className="chat-messages">
        {messages.map(({ sender, color, message, timestamp }) => (
          <div className="chat-message" key={timestamp}>
            <div className="chat-message-header">
              <strong style={{ color }}>{sender}</strong>
              <span>{new Date(timestamp).toLocaleString("en-US")}</span>:
            </div>
            <div>{message}</div>
          </div>
        ))}
      </div>
      <div className="chat-reply">
        <input
          type="text"
          placeholder={"Write as " + username}
          value={reply}
          onChange={(ev) => setReply(ev.target.value)}
        />
      </div>
    </form>
  );
}

export default ChatScreen;
