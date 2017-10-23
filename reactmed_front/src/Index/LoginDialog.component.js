import React from 'react';
import LoginForm from "./LoginForm.component";
import ModalDialog from "../Common/Components/Dialog.component";
import DialogHeader from "../Common/Components/DialogHeader.component";
import DialogBody from "../Common/Components/DialogBody.component";
import DialogFooter from "../Common/Components/DialogFooter.component";

class LoginDialog extends React.Component {
    render() {
        return (
            <ModalDialog>
                <DialogHeader title="Войти"/>
                <DialogBody>
                    <div className="row">
                        <div className="login-dialog">
                            <ul className="nav nav-tabs">
                                <li className="active"><a href="#login" data-toggle="tab">Войти</a></li>
                            </ul>
                            <div className="tab-content">
                                <div className="tab-pane active">
                                    <LoginForm/>
                                </div>
                            </div>
                        </div>
                    </div>
                </DialogBody>
                <DialogFooter>
                    <a href="">Забыли пароль?</a>
                </DialogFooter>
            </ModalDialog>
        );
    }
}

export default LoginDialog;