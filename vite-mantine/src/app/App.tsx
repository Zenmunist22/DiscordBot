import "@mantine/core/styles.css";
import { MantineProvider } from "@mantine/core";
import { theme } from "../theme";
import Root from "./Root";



export default function App() {
  return <MantineProvider theme={theme}>
      <Root></Root>
    </MantineProvider>;
}
