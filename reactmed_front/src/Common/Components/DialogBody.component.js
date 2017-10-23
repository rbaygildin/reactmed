import React from 'react';

export default class DialogBody extends React.Component{
    render(){
        return(
            <div className="modal-body">
                {this.props.children}
            </div>
        );
    }
}