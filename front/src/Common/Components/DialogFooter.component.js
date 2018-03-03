import React from 'react';

export default class DialogFooter extends React.Component{
    render(){
        return(
            <div className="modal-footer">
                {this.props.children}
            </div>
        );
    }
}