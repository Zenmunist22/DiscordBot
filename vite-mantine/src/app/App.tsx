import "@mantine/core/styles.css";
import { Container, MantineProvider } from "@mantine/core";
import { theme } from "../theme";
import { Link, Outlet } from "react-router-dom";



export default function App() {
  return ( 
    <MantineProvider theme={theme}>
      
      <Container fluid style= {{height: '95vh'}}bg="var(--mantine-color-blue-light)" >
        <Link to="/"> Home </Link>
        <Link to="/register"> Register </Link>
        <Link to="/login"> Login </Link>
        <Outlet></Outlet>    
      </Container>
    </MantineProvider>
  );
}
