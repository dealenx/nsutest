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
import ButtonGroup from 'react-bootstrap/lib/ButtonGroup'
import NavItem from 'react-bootstrap/lib/NavItem'
import Nav from 'react-bootstrap/lib/Nav'
import Panel from 'react-bootstrap/lib/Panel'
import ButtonToolbar from 'react-bootstrap/lib/ButtonToolbar'
import PanelGroup from 'react-bootstrap/lib/PanelGroup'
import Label from 'react-bootstrap/lib/Label'
import Tabs from 'react-bootstrap/lib/Tabs'
import Tab from 'react-bootstrap/lib/Tab'
import Table from 'react-bootstrap/lib/Table'

export default class App extends Component {
    constructor() {
        super();
        this.state = {
            username: sessionStorage.getItem('username'),
            loggedIn: !!sessionStorage.getItem('token'),
            tasks: [],
            compilers: [],
            compiler_id: '1',
            task_id: '1',
            loading: false,
            alerts: [],
            status: {
                filename: null,
                source: null
            },
            status_signin: {
                login: null,
                password: null
            },
            file: null,
            submitList: [],
            ratingList: [],
            activeKey: null
        };
        this.signIn = this.signIn.bind(this);
        this.signUp = this.signUp.bind(this);
        this.signOut = this.signOut.bind(this);
        this.sendProgram = this.sendProgram.bind(this);
        this.generateAlert = this.generateAlert.bind(this);
        this.reloadCompilers = this.reloadCompilers.bind(this);
        this.onSelectCompiler = this.onSelectCompiler.bind(this);
        this.onSelectTask = this.onSelectTask.bind(this);
        this.getSubmitList = this.getSubmitList.bind(this);
        this.getRatingList = this.getRatingList.bind(this);
        this.deleteSubmit = this.deleteSubmit.bind(this);
        this.getResultColor = this.getResultColor.bind(this);
        this.setActiveKey = this.setActiveKey.bind(this);
    }

    setActiveKey(key) {
        this.setState({ activeKey : key })
    }

    getResultColor(result){
        let color = 'info';
        if (result === "OK") color = "success";
        if (result === "RUNTIME_ERROR"
            || result === "TIME_LIMIT"
            || result === "MEMORY_LIMIT"
            || result === "SYSTEM_TIME_LIMIT"
            || result === "SECURITY_VIOLATION"
            || result === "WRONG_ANSWER"
            || result === "INVALID_INPUT"
            || result === "COMPILATION_ERROR") color = "danger";
        return color;
    }

    getSubmitList(){
        let self = this;
        axios.post('/get_tested_list', { username : sessionStorage.getItem('username') })
            .then(function(response) {
                self.setState({
                    submitList : response.data !== null ?
                        response.data
                            .map((submit) =>
                                <Panel id="submit"
                                       eventKey={submit.commit_id}
                                       bsStyle={self.getResultColor(submit.result_code)}
                                       key={submit.commit_id}>
                                    <Panel.Heading>
                                        <Panel.Title toggle>
                                        {submit.filename + '  '}
                                        </Panel.Title>
                                    </Panel.Heading>
                                    <Panel.Body collapsible>
                                        <p>Status: {submit.status}</p>
                                        <p>Submit time: {submit.commit_time}</p>
                                        <p>Result code: {'  '}
                                            <Label bsStyle={self.getResultColor(submit.result_code)}>
                                                {submit.result_code}
                                            </Label>
                                        </p>
                                        {"Output: "}
                                        <Well bsSize='sm'>{submit.output}</Well>
                                        <ButtonToolbar>
                                            <Button bsSize="small" bsStyle="danger" onClick={() => self.deleteSubmit(submit.commit_id)}>
                                                Delete submit
                                            </Button>
                                        </ButtonToolbar>
                                    </Panel.Body>
                                </Panel>
                            )
                        : []
                });
            })
    }

    getRatingList(){
        let self = this;
        axios.get('get_statistics')
            .then(function(response) {
                self.setState({
                    ratingList : response.data !== null ?
                        response.data.map((row) =>
                            <tr>
                                <td>{row.username}</td>
                                <td>{row.score}</td>
                            </tr>
                        ) 
                    : []
                });
            })
    }

    deleteSubmit(id) {
        let self = this;
        axios.post('/delete_submit', { 'submit_id' : id })
            .then(function(response) {
                self.getSubmitList();
            })
    }

    onSelectCompiler(e) {
        const selectedCompilerIndex = e.target.options.selectedIndex;
        this.setState({
            compiler_id: e.target.options[selectedCompilerIndex].getAttribute('datakeycompiler')
        });
    }

    onSelectTask(e) {
        const selectedTaskIndex = e.target.options.selectedIndex;
        this.setState({
            task_id: e.target.options[selectedTaskIndex].getAttribute('datakey')
        });
    }

    componentWillMount() {
        this.reloadTasks();
        this.reloadCompilers();
        this.getRatingList();
        if (!sessionStorage.getItem('token'))
            this.signOut();
        else this.getSubmitList();
    }

    reloadTasks() {
        let self = this;
        axios.get('/tasks')
            .then(function(response) {
                self.setState({
                    tasks: response.data
                        .map((task) => <option key={task.name} datakey={task.id} value={task.name}>{task.name}</option>)
                })
            });
    }

    reloadCompilers() {
        let self = this;
        axios.get('/compilers')
            .then(function(response) {
                self.setState({
                    compilers: response.data
                        .map((compiler) =>
                            <option key={compiler.id} datakeycompiler={compiler.id} value={compiler.name}>
                                {compiler.name}
                            </option>)
                })
            })
    }

    signIn(){
        let self = this;
        const credentials = {
            login: document.getElementById("login-form").value,
            password: document.getElementById("password-form").value
        };
        let login_status = '';
        let password_status = '';
        if (credentials.login === '') login_status = 'error';
        if (credentials.password === '') password_status = 'error';
        this.setState({ status_signin: { login : login_status, password : password_status } });
        if (credentials.login !== '' && credentials.password !== '') {
            axios.post('/auth/login', credentials)
                .then(function (response) {
                    self.setState({ status_signin: { login : null, password : null } });
                    self.setState({loggedIn: true, username: credentials.login});
                    sessionStorage.setItem('username', credentials.login);
                    sessionStorage.setItem('token', response.data.token);
                    self.getSubmitList();
                });
        }
    }

    verifyUser() {
        axios({
            method: 'POST',
            url: '/auth/verify',
            headers: { authorization: sessionStorage.getItem('token') },
            data: { 'username' : this.state.username }
        })
            .then(function(response) {
                if (response.status === 400) this.signOut();
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



    sendProgram() {
        this.verifyUser();
        const data = {
            filename: document.getElementById("fileName").value,
            username: this.state.username,
            task_id: this.state.task_id,
            compiler_id: this.state.compiler_id,
            source: document.getElementById("programCode").value
        };
        let filename_status = '';
        let source_status = '';
        if (data.filename === '') filename_status = 'error';
        if (data.source === '') source_status = 'error';
        this.setState({ status: { filename : filename_status, source : source_status } });
        if (data.filename !== '' && data.source !== '') {
            this.setState({ loading : true });
            let self = this;
            axios.post('/compile', data)
                .then(function (response) {
                    console.log(response);
                    self.setState({ loading : false, status : { filename : '', source : '' } });
                    self.generateAlert('success', 'Program sent successfully');
                })
                .catch(function (error) {
                    console.log(error);
                    self.setState({ loading : false });
                    self.generateAlert('danger', 'Error. Please, try again');
                });
        }
        this.getSubmitList();
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
                        <FormGroup controlId="login-form" validationState={this.state.status_signin.login}>
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
                        <FormGroup controlId="password-form" validationState={this.state.status_signin.password}>
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
            <Tabs defaultActiveKey={1} id="main-tab">
                <Tab eventKey={1} title="Send submit">
                <div>
                    <Well>
                        <FormGroup controlId="taskName">
                            <ControlLabel>Choose task</ControlLabel>
                            <FormControl componentClass="select" onChange={this.onSelectTask}>
                                {this.state.tasks}
                            </FormControl>
                        </FormGroup>
                        <FormGroup controlId="fileName" validationState={this.state.status.filename}>
                            <ControlLabel>Enter the file name</ControlLabel>
                            <FormControl
                                required
                                type="text"
                                placeholder="Enter text"
                            />
                            <FormControl.Feedback />
                            <HelpBlock>If you insert your code into the form below</HelpBlock>
                        </FormGroup>
                        <FormGroup controlId="programCode" validationState={this.state.status.source}>
                            <ControlLabel>Code area</ControlLabel>
                            <FormControl componentClass="textarea" placeholder="Paste your code here" />
                        </FormGroup>
                        <FormGroup controlId="file">
                            <ControlLabel>Upload file</ControlLabel>
                            <FormControl componentClass="input" type="file" id="file" name="file" onChange={this.uploadFile} />
                            <HelpBlock>Attach file without copying</HelpBlock>
                        </FormGroup>
                        <FormGroup controlId="compilerName">
                            <ControlLabel>Choose compiler</ControlLabel>
                            <FormControl componentClass="select" onChange={this.onSelectCompiler}>
                                {this.state.compilers}
                            </FormControl>
                        </FormGroup>
                        <Button type="submit" disabled={this.state.loading} onClick={this.sendProgram}>
                            {this.state.loading ? 'Loading...' : 'Send to server'}
                        </Button>
                    </Well>
                    <PanelGroup id='submitList' activeKey={this.state.activeKey} onSelect={this.setActiveKey} accordion>
                        {this.state.submitList}
                    </PanelGroup>
                </div>
                </Tab>
                <Tab eventKey={2} title="User rating">
                <Well>
                    <Table responsive>
                        <thead>
                            <th>Username</th>
                            <th>Completed tasks number</th>
                        </thead>
                        <tbody>
                            {this.state.ratingList}
                        </tbody>
                    </Table>
                </Well>
                </Tab>
            </Tabs>
            </Grid>
        </div>;
    }
}
