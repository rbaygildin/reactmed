import React from 'react';
import './index.css';
import Menu from "./Menu.component";
import LoginDialog from "./LoginDialog.component";

class Index extends React.Component{
    render(){
        return (
            <div className="container">
                <Menu/>
                <LoginDialog/>
            </div>
        );
    }
}

export default Index;