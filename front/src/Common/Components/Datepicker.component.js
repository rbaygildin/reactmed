import React from 'react';

export default class DatePicker extends React.Component{
    render(){
        return(
            <div>
                <label className={'datepicker control-label col-md-' + this.props.titleCol} htmlFor={'id_' + this.props.name + '_input'}>{this.props.title}</label>
                <div className={'col-md-' + this.props.inputCol}>
                    <input id={'id_' + this.props.name + '_input'} name={this.props.name} className="form-control"/>
                </div>
            </div>
        );
    }
}