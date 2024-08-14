import { TextInput } from "@mantine/core";
import { Form, useSubmit } from "react-router-dom";

export default function Login() {
    const submit = useSubmit();
    return <>
        <Form method="post" action="../app/Root" onSubmit={(event) => {submit(event.currentTarget)}}>
            <TextInput radius="md" label="Input label" description="Input description"  name="title"  />
            <button type="submit">Create</button>
        </Form>
    </>

}