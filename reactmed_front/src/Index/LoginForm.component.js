import React from 'react';
import Input from "../Common/Components/Input.component";
import Password from "../Common/Components/Password.component";
import Button from "../Common/Components/Button.component";

class LoginForm extends React.Component {
    onSubmit(event){
        event.preventDefault();
        event.stopPropagation();
    }
    render() {
        return (
            <form id="id_login_form" action=""
                  className="form-horizontal" method="post" onSubmit={this.onSubmit}>
                <div className="form-group">
                    <Input titleCol="2" inputCol="10" name="username" title="Логин" icon="user"/>
                </div>
                <div className="form-group">
                    <Password titleCol="2" inputCol="10" name="username" title="Пароль" icon="lock"/>
                </div>
                <div className="row pull-right">
                    <Button title="Войти" col="4" color="primary"/>
                    <Button title="Регистрация" col="8" color="primary"/>
                </div>
            </form>
        );
    }
}

export default LoginForm;