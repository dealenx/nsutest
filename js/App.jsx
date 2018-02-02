import React, { Component } from 'react'
import axios from 'axios'
import { AlertList } from "react-bs-notifier"

import Button from 'react-bootstrap/lib/Button'
import Well from 'react-bootstrap/lib/Well'
import Grid  from 'react-bootstrap/lib/Grid'
import Modal  from 'react-bootstrap/lib/Modal'
import Navbar  from 'react-bootstrap/lib/Navbar'
import FormGroup from 'react-bootstrap/lib/FormGroup'
import ControlLabel from 'react-bootstrap/lib/ControlLabel'
import FormControl from 'react-bootstrap/lib/FormControl'
import Form from 'react-bootstrap/lib/Form'
import Col from 'react-bootstrap/lib/Col'
import HelpBlock from 'react-bootstrap/lib/HelpBlock'
import ButtonGroup from "react-bootstrap/lib/ButtonGroup"
import NavItem from "react-bootstrap/lib/NavItem"
import Nav from "react-bootstrap/lib/Nav"


export default class App extends Component {
    constructor() {
        super();
        this.state = {
            username: sessionStorage.getItem('username'),
            loggedIn: !!sessionStorage.getItem('token'),
            tasks: null,
            compilers: null,
            loading: false,
            alerts: []
        };
        this.signIn = this.signIn.bind(this);
        this.signUp = this.signUp.bind(this);
        this.signOut = this.signOut.bind(this);
        this.sendProgram = this.sendProgram.bind(this);
        this.generateAlert = this.generateAlert.bind(this);
    }

    componentWillMount() {
        if (!sessionStorage.getItem('token')) {
            this.setState({ loggedIn : false })
            // this.reloadTasks();
            // this.reloadCompilers();
        }
    }

    reloadTasks() {
        axios.get('/tasks')
            .then(function(response) {
                self.setState({
                    firstFields: response.data
                        .map((name) => <option key={name} value={name}>{name}</option>)
                })
            });
    }

    reloadCompilers() {
        axios.get('/compilers')
            .then(function(response) {
                self.setState({
                    firstFields: response.data
                        .map((name) => <option key={name} value={name}>{name}</option>)
                })
            });
    }

    signIn() {
        let self = this;
        const credentials = {
            login: document.getElementById("login-form").value,
            password: document.getElementById("password-form").value
        };
        axios.post('/auth/login', credentials)
            .then(function(response) {
                self.setState({ loggedIn : true, username: credentials.login });
                sessionStorage.setItem('username', credentials.login);
                sessionStorage.setItem('token', response.data.token);
            });
    }

    verifyUser() {
        axios({
            method: 'POST',
            url: '/auth/verify',
            headers: { authorization: sessionStorage.getItem('token') },
            data: { 'username' : this.state.username }
        })
            .then(function(response) {
                if (response.status === 200)
                    console.log(response.data);
                if (response.status === 400)
                    this.signOut();
            });
    }

    signUp() {
        const credentials = {
            login: document.getElementById("login-form").value,
            password: document.getElementById("password-form").value
        };
        axios.post('/auth/register', credentials)
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    signOut() {
        this.setState({ loggedIn : false, username : null });
        sessionStorage.clear();
    }

    sendProgram(e) {
        this.verifyUser();
        this.setState({ loading : true });
        // let file_ = new FormData();
        // file_.append('file', e.target.files[0]);
        const data = {
            filename: document.getElementById("fileName").value,
            username: this.state.username,
            task_id: "1",//document.getElementById("taskName").value,
            compiler_id: "1",//document.getElementById("compilerName").value,
            source: document.getElementById("programCode").value,
            // file: file_
        };
        let self = this;
        axios.post('/compile', data)
            .then(function (response) {
                console.log(response);
                self.setState({ loading : false });
                self.generateAlert("success", "Tests passed");
            })
            .catch(function (error) {
                console.log(error);
                self.setState({ loading : false });
                self.generateAlert("danger", "Tests failed. Please, try again");
            });
    }

    generateAlert(type, massage) {
        const newAlert = {
            id: (new Date()).getTime(),
            type: type,
            message: massage
        };
        this.setState({ alerts: [...this.state.alerts, newAlert] });
    }

    onAlertDismissed(alert) {
        const alerts = this.state.alerts;
        const idx = alerts.indexOf(alert);
        if (idx >= 0)
            this.setState({ alerts: [...alerts.slice(0, idx), ...alerts.slice(idx + 1)] });
    }

    render () {
        return <div>
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#">NSU-test-app</a>
                    </Navbar.Brand>
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav pullRight>
                        <NavItem onClick={this.signOut}>
                            {this.state.loggedIn ? "Log out" : ""}
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
            <AlertList
                position="bottom-right"
                alerts={this.state.alerts}
                timeout={2500}
                onDismiss={this.onAlertDismissed.bind(this)}
            />
            <Modal show={!this.state.loggedIn}>
                <Modal.Header>
                    <Modal.Title> Please, <strong>sign in</strong> to continue </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form horizontal>
                        <FormGroup controlId="login-form">
                            <Col  sm={2}>
                                Login
                            </Col>
                            <Col sm={10}>
                                <FormControl
                                    controlid="login"
                                    type="text"
                                    placeholder="Login"
                                />
                                <FormControl.Feedback />
                            </Col>
                        </FormGroup>

                        <FormGroup controlId="password-form">
                            <Col  sm={2}>
                                Password
                            </Col>
                            <Col sm={10}>
                                <FormControl
                                    controlid="password"
                                    type="password"
                                    placeholder="Password"
                                />
                                <FormControl.Feedback />
                            </Col>
                        </FormGroup>
                        
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <ButtonGroup>
                        <Button onClick={this.signIn}>Sign in</Button>
                        <Button onClick={this.signUp}>Registration</Button>
                    </ButtonGroup>
                </Modal.Footer>
            </Modal>
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
                            <input value="" type="file" id="file" name="file" />
                            <HelpBlock>Attach file without copying</HelpBlock>
                        </FormGroup>
                        <FormGroup controlId="compilerName">
                            <ControlLabel>Choose compiler</ControlLabel>
                            <FormControl componentClass="select">
                                {this.state.compilers}
                            </FormControl>
                        </FormGroup>
                        <Button type="submit" disabled={this.state.loading} onClick={this.sendProgram}>
                            {this.state.loading ? 'Loading...' : 'Send to server'}
                        </Button>
                    </Well>
                </div>
            </Grid>

        </div>;
    }
}
