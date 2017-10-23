import React from 'react';

export default class DialogHeader extends React.Component{
    render(){
        return (
            <div className="modal-header">
                <button type="button" className="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 className="modal-title">{this.props.title}</h4>
            </div>
        );
    }
}