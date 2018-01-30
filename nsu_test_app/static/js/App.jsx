import React, { Component } from 'react'
import axios from 'axios'

import Button from 'react-bootstrap/lib/Button'
import PageHeader from 'react-bootstrap/lib/PageHeader'
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
        let file_ = new FormData();
        file_.append('file', e.target.files[0]);
        const data = {
            task: document.getElementById("taskName").value,
            text: document.getElementById("textarea").value,
            file: file_,
            compiler: document.getElementById("compilerName").value
        };
        axios.post('/program/', data)
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
                <PageHeader>Check task <small>using nsu-test-app</small></PageHeader>
                <div>
                    <Well bsSize="large">
                        <FormGroup controlId="taskName">
                            <ControlLabel>Choose task</ControlLabel>
                            <FormControl componentClass="select">
                                {this.state.tasks}
                            </FormControl>
                        </FormGroup>
                        <FormGroup controlId="formControlsTextarea">
                            <ControlLabel>Code area</ControlLabel>
                            <FormControl componentClass="textarea" placeholder="Paste your code here" />
                        </FormGroup>
                        <FormGroup controlId="formControlsFile">
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