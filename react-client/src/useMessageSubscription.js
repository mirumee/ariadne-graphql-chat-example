import { useSubscription, gql } from "@apollo/client";

const MESSAGE_SUBSCRIPTION = gql`
  subscription GetMessage {
    message {
      sender
      color
      message
      timestamp
    }
  }
`;

function useMessageSubscription(onData) {
  return useSubscription(MESSAGE_SUBSCRIPTION, {
    onData,
    shouldResubscribe: true,
  });
}

export default useMessageSubscription;
