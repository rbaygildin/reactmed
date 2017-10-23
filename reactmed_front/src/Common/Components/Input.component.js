import React from 'react';

class Input extends React.Component{
    render(){
        return (
            <div>
                <label className={'control-label col-md-' + this.props.titleCol} htmlFor={'id_' + this.props.name + '_input'}>{this.props.title}</label>
                <div className={'col-md-' + this.props.inputCol}>
                    <input id={'id_' + this.props.name + '_input'} name={this.props.name} className="form-control"/>
                </div>
            </div>
        );
    }
}

Input.defaultProps = {
    titleCol: '2',
    inputCol: '4'
};

export default Input;