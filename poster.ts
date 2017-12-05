#!/usr/bin/env node

/**
 * File: poster.ts
 * ---------------
 * This program is for posting data to some web service. It will post the contents
 * of all files matching a specified regex in a specified directory to the specified
 * URI asynchronously.
 */

import http = require('http');
import fs = require('fs');
import command_line_args = require('command-line-args');

// command line parsing
const option_definitions = [
  { name: 'verbose',    alias: 'v', type: Boolean,                  defaultOption: false },
  { name: 'directory',              type: String,  multiple: false, defaultValue: './' },
  { name: 'regex',      alias: 'r', type: String,                   defaultValue: '.*'},
  { name: 'host',       alias: 'h', type: String,                   defaultValue: 'localhost'},
  { name: 'port',       alias: 'p', type: Number,                   defaultValue: 3000},
  { name: 'route',      alias: 't', type: String},
  { name: 'method',     alias: 'm', type: String,                   defaultValue: 'POST'}
];
const options = command_line_args(option_definitions);
console.log(`route: ${options.route}`);
const post_options = {
  host: options.host,
  port: options.port,
  path: options.route,
  method: options.method,
  headers: undefined
};
const regex = new RegExp(options.regex); // Create the regex for searching

if (options.verbose) {
  console.log(`${options.method}-ing from dir: \"${options.directory}\" matching: \"${options.regex}\"`);
  console.log(`Posting to: ${options.host}:${options.port}${options.route}`);
}

fs.readdir(options.directory, (dir_error, files) => {
  if (dir_error) { console.error(`Error reading: ${options.directory}`); return; }
  files.forEach(file => {
    if (file.match(regex)) {
      fs.readFile(file, (file_error, data) => {
        if (file_error) { console.error(`Error reading: ${file}`); return; }
        const data_length = Buffer.byteLength(data.toString());
        // Set headers correctly
        post_options.headers = {
          'Content-Type': 'application/json',
          'Content-Length': data_length
        };
        // post the contents
        const post_req = http.request(post_options, res => {
          res.setEncoding('utf8');
          res.on('data', response => console.log(`\tPosted file: ${file}, response: ${response}`));
        });
        post_req.write(data);
        post_req.end();
      });
    }
  });
});
