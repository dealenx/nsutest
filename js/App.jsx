import React, { Component } from 'react'
import axios from 'axios'

import Button from 'react-bootstrap/lib/Button'
import Well from 'react-bootstrap/lib/Well'
import Grid  from 'react-bootstrap/lib/Grid'
import Navbar  from 'react-bootstrap/lib/Navbar'
import FormGroup from 'react-bootstrap/lib/FormGroup'
import ControlLabel from 'react-bootstrap/lib/ControlLabel'
import FormControl from 'react-bootstrap/lib/FormControl'
import HelpBlock from 'react-bootstrap/lib/HelpBlock'


export default class App extends Component {
    constructor() {
        super();
        this.state = {
            tasks: null,
            compilers: null,
        };
        this.reloadTasks = this.reloadTasks.bind(this);
        this.reloadCompilers = this.reloadCompilers.bind(this);
    }

    reloadTasks() {
        let self = this;
        let taskName = document.getElementById("taskName").value;
        axios.get('/tasks/?taskName=' + taskName)
            .then(function(response) {
                self.setState({
                    firstFields: response.data
                        .map((name) => <option key={name} value={name}>{name}</option>)
                })
            });
    }

    reloadCompilers() {
        let self = this;
        let compilerName = document.getElementById("compilerName").value;
        axios.get('/compilers/?compilerName=' + compilerName)
            .then(function(response) {
                self.setState({
                    firstFields: response.data
                        .map((name) => <option key={name} value={name}>{name}</option>)
                })
            });
    }

    sendProgram(e) {
        // let file_ = new FormData();
        // file_.append('file', e.target.files[0]);
        const data = {
            file_name: document.getElementById("fileName").value,
            uid: "1",
            task_id: "1",//document.getElementById("taskName").value,
            lang: "2",//document.getElementById("compilerName").value,
            source: document.getElementById("programCode").value,
            // file: file_
        };
        axios.post('/load_program', data)
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    render () {
        return <div>
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#">NSU-test-app</a>
                    </Navbar.Brand>
                </Navbar.Header>
            </Navbar>
            <Grid>
                <div>
                    <Well bsSize="large">
                        <FormGroup controlId="taskName">
                            <ControlLabel>Choose task</ControlLabel>
                            <FormControl componentClass="select">
                                {this.state.tasks}
                            </FormControl>
                        </FormGroup>
                        <FormGroup controlId="fileName">
                            <ControlLabel>Enter the file name</ControlLabel>
                            <FormControl
                                type="text"
                                placeholder="Enter text"
                            />
                            <FormControl.Feedback />
                            <HelpBlock>If you insert your code into the form below</HelpBlock>
                        </FormGroup>
                        <FormGroup controlId="programCode">
                            <ControlLabel>Code area</ControlLabel>
                            <FormControl componentClass="textarea" placeholder="Paste your code here" />
                        </FormGroup>
                        <FormGroup controlId="file">
                            <ControlLabel>Upload file</ControlLabel>
                            <input type="file" id="file" name="file" />
                            <HelpBlock>Attach file without copying</HelpBlock>
                        </FormGroup>
                        <FormGroup controlId="compilerName">
                            <ControlLabel>Choose compiler</ControlLabel>
                            <FormControl componentClass="select">
                                {this.state.compilers}
                            </FormControl>
                        </FormGroup>
                        <Button onClick={() => this.sendProgram()}> Send to server </Button>
                    </Well>
                </div>
            </Grid>
        </div>;
    }
}
