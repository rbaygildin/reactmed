class TestSelect extends React.Component {
            constructor(props) {
                super(props);

                this.state = {
                    tests: []
                };
            }

            componentDidMount() {
                $.get('{% url "api:tests" %}', tests => {
                    console.log(tests);
                    this.setState({tests: tests});
                });
            }

            change(event){
                console.log(event.target.value);
            }

            render() {
                return (
                    <select>
                    </select>
                        this.state.tests.map(test => {
                                return <option value={test['short_name']}>{test.name}</option>
                        })
                );
            }
}