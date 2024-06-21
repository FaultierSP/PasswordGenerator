import { writeText } from '@tauri-apps/api/clipboard';

import { useState, useEffect, useRef } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import "./App.css";

import { Col, Row, Flex, Card, Tooltip,
          Button, Input, InputNumber, Form, Checkbox,
          message } from "antd";

function App() {
  const labelCol={style: {
    width:180,
  }};

  const numberOfPasswordInputs=3;
  const [formHandle]=Form.useForm();
  const initialValues={
    numberOfChunks:2,
    digitsPerChunk:4,
    numberOfSyllables:4,
  };
  const [messageApi,contextHolder]=message.useMessage();

  const showSuccessMessage = () => {
    messageApi.open({
      type:'success',
      content:'Copied to clipboard',
      style: {
        marginTop: '50%',
      }
    });
  }

  const showPasswordInputs = () => {
    let returnBuffer=[];

    for (let i=0;i<numberOfPasswordInputs;i++) {
      returnBuffer.push(
        <Tooltip title="Click to copy"><Form.Item name={["passwordInput",i]}>
          <Input onClick={copyToClipboard} id={"key_"+i} readOnly/>
        </Form.Item></Tooltip>
      );
    }
    return returnBuffer;
  }

  const fillPasswords = () => {
    let numberOfChunks=formHandle.getFieldValue("numberOfChunks");
    let numberOfSyllables=formHandle.getFieldValue("numberOfSyllables");
    let digitsPerChunk=formHandle.getFieldValue("digitsPerChunk");
    let includeSpecialCharacters=(typeof(formHandle.getFieldValue("specialCharacters"))=="undefined" ? true : formHandle.getFieldValue("specialCharacters"));
    let varySlightly=(typeof(formHandle.getFieldValue("varySlightly"))=="undefined" ? true : formHandle.getFieldValue("varySlightly"));

    for (let i=0;i<numberOfPasswordInputs;i++) {
      invoke("send_a_password_to_the_frontend", {numberOfChunks, numberOfSyllables, digitsPerChunk,includeSpecialCharacters,varySlightly} ).then(
        (response) => {
          formHandle.setFieldValue(["passwordInput",i],response);
        }
      )
    }
  }

  const copyToClipboard = (event) => {
    writeText(document.getElementById(event.target.id).value).then(showSuccessMessage());
  } 

  const sendCloseSignal = () => {
    invoke("exit_app");
  }

  useEffect(()=>{
    fillPasswords();
  },[]);

  return (
    <Form form={formHandle} initialValues={initialValues} name="passwordsForm">
    {contextHolder}
    <Flex vertical gap="middle">
        <Card>
          <Flex vertical gap={1}>
            {showPasswordInputs()}
          </Flex>
        </Card>
        <Card>
        <Row>
          <Col span={12}>
            <Form.Item label="Number of chunks" labelCol={labelCol} name={"numberOfChunks"}>
              <InputNumber min={1} max={7} changeOnWheel/>
            </Form.Item>
            <Form.Item label="Number of syllables" labelCol={labelCol} name={"numberOfSyllables"}>
              <InputNumber min={1} max={7} changeOnWheel/>
            </Form.Item>
            <Form.Item label="Digits per chunk" labelCol={labelCol} name={"digitsPerChunk"}>
              <InputNumber min={1} max={7} changeOnWheel/>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item label="Special characters" labelCol={labelCol} name={"specialCharacters"} valuePropName="checked">
              <Checkbox defaultChecked={true}/>
            </Form.Item>
            <Form.Item label="Vary slightly" labelCol={labelCol} name={"varySlightly"} valuePropName="checked">
              <Checkbox defaultChecked={true}/>
            </Form.Item>
          </Col>
        </Row>
        </Card>
      <Flex gap="middle" justify="center" align="center">
        <Button onClick={fillPasswords}>New passwords</Button>
        <Button onClick={sendCloseSignal}>Bye-bye</Button>
      </Flex>
    </Flex>
    </Form>
)};

export default App;
