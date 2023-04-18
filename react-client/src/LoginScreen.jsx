import * as React from "react";

function LoginScreen({ setUsername }) {
  const [value, setValue] = React.useState("");

  return (
    <form
      className="login-form"
      onSubmit={(ev) => {
        const username = value.trim();
        if (username.length > 0) {
          setUsername(username);
        }

        ev.preventDefault();
        return false;
      }}
    >
      <label htmlFor="username">Username:</label>
      <input
        type="text"
        value={value}
        onChange={(ev) => setValue(ev.target.value)}
      />
      <button type="submit">Sign In</button>
    </form>
  );
}

export default LoginScreen;
