import { useQuery, gql } from "@apollo/client";

const GET_HISTORY = gql`
  query GetHistory {
    history {
      sender
      color
      message
      timestamp
    }
  }
`;

function useHistoryQuery() {
  return useQuery(GET_HISTORY);
}

export default useHistoryQuery;
