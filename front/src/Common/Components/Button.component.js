import React from 'react';

class Button extends React.Component{
    render(){
        return (
          <button className={'btn btn-' + this.props.color + ' col-md-' + this.props.col + ' ' + (this.props.className || '')}
                  onClick={this.props.onClick}>
              {this.props.title}
          </button>
        );
    }
}

Button.defaultProps = {
    col: '2',
    color: 'success'
};

export default Button;