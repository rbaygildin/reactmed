import React from 'react';
import Input from "../Common/Components/Input.component";
import Password from "../Common/Components/Password.component";
import Button from "../Common/Components/Button.component";

class LoginForm extends React.Component{
   render(){
       return(
           <form>
               <div className="form-group row">
                   <Input title="Login" name="username"/>
               </div>
               <div className="form-group row">
                   <Password/>
               </div>
               <div className="form-group row">
                   <Button title="Log In"/>
               </div>
           </form>
       );
   }
}

export default LoginForm;