class TestOptions extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tests: []
        };
    }
    
    render() {
        let options = this.props.tests.map(test => {
                    return <option value = {test['short_name']}> {test.name} </option>
        });
        return (
            options
        );
    }
}