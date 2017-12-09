class TestSelect extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tests: []
        };
    }

    change(event) {
        console.log(event.target.value);
    }

    render() {
        return ( <select className = "form-control" onChange = {this.change}> 
                {
                this.props.tests.map(test => {
                    return <option value = {test['short_name']}> {test.name} </option>
                })
            } </select>
        );
    }
}