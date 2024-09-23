import { Box, Button, Center, Group, TextInput, Image, PasswordInput, Title} from "@mantine/core";
import { Form } from "react-router-dom";
import { useForm } from "@mantine/form";
import this_is_fine from "../../assets/images/this-is-fine.gif";
import { FormEvent } from "../types";

export default function Login() {
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            firstname: '',
            lastname: '',
            email: '',
            phonenumber: '',
            username: '',
            password: '',
        },
    
        validate: {
            firstname: (value) => (value.length < 2 ? 'First Name must have at least 2 letters' : null),
            lastname: (value) => (value.length < 2 ? 'Last Name must have at least 2 letters' : null),
            email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
            phonenumber: (value) => (value.length < 2 ? 'Phone Number must have at least 2 characters' : null),
            username: (value) => (value.length < 2 ? 'Username must have at least 2 letters' : null),
            password: (value) => (value).length < 2 ? 'Your password needs at least length of 2.' : null,
        },
    });

    const handleSubmit = async (event:FormEvent) => {
        form.validate();
        if (!form.isValid()){
            return <p> Error </p>;
        }
        event.preventDefault();
        
        const formData = new FormData(event.currentTarget);
        const url = "http://localhost:5173/api/register";

        const payload = {

            firstname: formData.get("firstname")?.toString(),
            lastname: formData.get("lastname")?.toString(),
            email: formData.get("email")?.toString(),
            phonenumber: formData.get("phonenumber")?.toString(),
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
            <Box bg="var(--mantine-color-blue-light)" maw={600}  style={{width: '25%', height: 'auto'}} p={20} >

                <Title style={{ borderBottom:"2px solid var(--mantine-color-blue-light)"}} order={1}>Registration</Title>
                <Image
                    radius="md"
                    src={this_is_fine}
                    mah='200px'
                    style={{height:'70%'}}
                    mt={10}
                />
                <Form  method="post" action="/register" onSubmit={(event) => {handleSubmit(event)}}>
                    <Group justify="space-between" grow preventGrowOverflow={false}>
                        <TextInput 
                            radius="md" 
                            label="First Name" 
                            name="firstname" 
                            mt={10}
                            key={form.key('firstname')}
                            {...form.getInputProps('firstname')}
                             
                        />
                        <TextInput 
                            radius="md" 
                            label="Last Name"  
                            name="lastname"  
                            mt={10}
                            key={form.key('lastname')}
                            {...form.getInputProps('lastname')}
                             
                        />
                    </Group>
                    
                    <TextInput 
                        radius="md" 
                        label="Email" 
                        name="email"  
                        mt={10}
                        key={form.key('email')}
                        {...form.getInputProps('email')}
                         
                    />
                    <TextInput 
                        radius="md" 
                        label="Phone Number"  
                        name="phonenumber" 
                        mt={10}
                        key={form.key('phonenumber')}
                        {...form.getInputProps('phonenumber')}
                         
                    />
                    <TextInput 
                        radius="md" 
                        label="Username"  
                        name="username"  
                        mt={10}
                        key={form.key('username')}
                        {...form.getInputProps('username')}
                         
                    />
                    <PasswordInput 
                        radius="md" 
                        label="Password" 
                        name="password" 
                        mt={10} 
                        key={form.key('password')}
                        {...form.getInputProps('password')}
                         
                    />
                    <Group justify="flex-end">
                        <Button type="submit" mt={30}> Submit </Button>
                    </Group>
                    
                </Form>

                
            </Box>
        </Center>
        
    </>

}