import { useMutation, gql } from "@apollo/client";

const REPLY = gql`
  mutation Reply($sender: String!, $message: String!) {
    reply(sender: $sender, message: $message)
  }
`;

function useReplyMutation() {
  return useMutation(REPLY);
}

export default useReplyMutation;
