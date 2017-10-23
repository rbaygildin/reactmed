import React from 'react';

class Button extends React.Component{
    render(){
        return (
          <button className={'btn btn-success col-md-' + this.props.col}>{this.props.title}</button>
        );
    }
}

Button.defaultProps = {
    col: '2'
};

export default Button;