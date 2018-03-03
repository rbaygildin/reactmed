import React from 'react';

class Menu extends React.Component{
    render(){
        return(
            <nav className="navbar navbar-inverse navbar-fixed-top" role="navigation">
                <div className="container">
                    <div className="navbar-header">
                        <div className="navbar-brand">ReactMed</div>
                    </div>
                    <ul className="nav navbar-nav">
                        <li><a href="/">Главная</a></li>
                        <li><a href="">О сайте</a></li>
                        <li><a href="">Юридическая информация</a></li>
                        <li><a href="">Помощь</a></li>
                    </ul>
                    <ul className="nav navbar-nav navbar-right">
                        <li><a href="#" data-toggle="modal" data-target="#login-modal">Войти</a></li>
                    </ul>
                </div>
            </nav>
        );
    }
}

export default Menu;