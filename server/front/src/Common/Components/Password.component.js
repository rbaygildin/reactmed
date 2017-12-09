import React from 'react';

export default class Password extends React.Component{
    render(){
        if(this.props.icon){
            return (
                <div>
                    <label className={'control-label col-md-' + this.props.titleCol} htmlFor={'id_' + this.props.name + '_input'}>{this.props.title}</label>
                    <div className={'col-md-' + this.props.inputCol}>
                        <div className="input-group">
                            <span className="input-group-addon">
                                <i className={'glyphicon glyphicon-' + this.props.icon}/>
                            </span>
                            <input id={'id_' + this.props.name + '_input'} className="form-control"
                                   placeholder={this.props.title}
                                   name={this.props.name}  type="password"/>
                        </div>
                    </div>
                </div>
            );
        }
        return (
            <div>
                <label className={'control-label col-md-' + this.props.titleCol} htmlFor={'id_' + this.props.name + '_input'}>{this.props.title}</label>
                <div className={'col-md-' + this.props.inputCol}>
                    <input id={'id_' + this.props.name + '_input'} name={this.props.name} className="form-control" type="password"/>
                </div>
            </div>
        );
    }
}

Password.defaultProps = {
    title: 'Password',
    name: 'password',
    titleCol: '2',
    inputCol: '4'
};