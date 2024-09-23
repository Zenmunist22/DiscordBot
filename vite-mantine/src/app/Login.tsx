import { Box, Button, Center, Group, TextInput, Image, PasswordInput } from "@mantine/core";
import { Form } from "react-router-dom";
import { useForm } from "@mantine/form";
import this_is_fine from "../../assets/images/this-is-fine.gif";
import { FormEvent } from "../types";

export default function Login() {
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            username: '',
            password: '',
        },
    
        validate: {
          password: (value) => (value).length < 2 ? null : 'Your password needs at least length of 2.',
        },
    });

    const handleSubmit = async (event:FormEvent) => {
        event.preventDefault();
        
        const formData = new FormData(event.currentTarget);
        const url = "http://127.0.0.1:8788/api/login"//"https://house-79v.pages.dev/api/login";

        const payload = {
            username: formData.get("username")?.toString(),
            password: formData.get("password")?.toString()
        }
        
        const options = {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json'}
        }
        try{
            const response = await fetch(url, options);
            const jsonResponse = await response.json();
            console.log('JSON response', jsonResponse);
        }
        catch (err){
            console.log('Error', err);
        }
        
    }

    return <>
        <Center bg="var(--mantine-color-gray-light)" maw={2000} style={{height: "100%"}}>
            <Box bg="var(--mantine-color-blue-light)" maw={600} mah={500} style={{width: '25%', height: '65%'}} p={20}>
                <Image
                    radius="md"
                    src={this_is_fine}
                    mah='200px'
                    style={{height:'70%'}}
                />
                <Form  method="post" action="/login" onSubmit={(event) => {handleSubmit(event)}}>
                    <TextInput radius="md" label="Username"  name="username"  mt={10}/>
                    <PasswordInput 
                    radius="md" 
                    label="Password" 
                    name="password" 
                    mt={10} 
                    key={form.key('password')}
                    {...form.getInputProps('password')}/>
                    <Group justify="flex-end">
                        <Button type="submit" mt={30}> Submit </Button>
                    </Group>
                    
                </Form>
            </Box>
        </Center>
        
    </>

}