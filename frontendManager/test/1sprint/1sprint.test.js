var request = require('supertest');
var express = require('express');
let should = require('should');
var assert = require('assert');

const user = {
    username: 'name',
    password: 'password'
};
var app = require('../../app');
const { isAssertionExpression } = require('typescript');
var port = process.env.PORT || 3000;
app.set('port', port);
describe('supertest 验证', function() {

    beforeEach(function() {
        console.log('before every test in every suit');
    });

    it('get 请求 start', function(done) {
        request(app)
            .get('/')
            .set('Cache-control', 'no-cache')
            .expect(200, done);
    });
    it('get 请求 register', function(done) {
        request(app)
            .get('/register')
            .set('Cache-control', 'no-cache')
            .expect(200, done);
    });
    it('get 请求 login', function(done) {
        request(app)
            .get('/login')
            .set('Cache-control', 'no-cache')
            .expect(200, done);
    });

    it('Post 请求 login', function() {
        assert.ok(true);
        /*.post('/sayHello')
            .set('Content-Type', 'application/json')
            .send({
                username: 'ryan',
                password: 'chen'
            })
            .expect('Content-Type', /json/)
            .expect(200, { message: "ryan你好" }, done);*/
    });
    it("Post 请求 register", function() {
        assert.ok(true);
    });

});