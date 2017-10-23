import React from 'react';

export default class Dialog extends React.Component{
    render(){
        return(
            <div className="modal fade" id="login-modal" tabindex="-1" role="dialog" aria-hidden="true">
                <div className="modal-dialog modal-md">
                    <div className="modal-content">
                        {this.props.children}
                    </div>
                </div>
            </div>
        );
    }
}