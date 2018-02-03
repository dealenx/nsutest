const webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

const config = {
    entry:  [__dirname + '/src/index.jsx', __dirname + '/src/css/style.sass'],
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js'
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
        rules: [
            {
                test: /\.jsx?/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            { // css / sass / scss loader for webpack
              test: /\.(css|sass|scss)$/,
              use: ExtractTextPlugin.extract({
                use: ['css-loader', 'sass-loader'],
              })
            }
        ]
      },

    plugins: [
    new ExtractTextPlugin('bundle.css'),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),
  ]
};
module.exports = config;
