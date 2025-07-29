const path = require('path');
// webpack needs to be explicitly required
const webpack = require('webpack')
//css minification
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const FixStyleOnlyEntriesPlugin = require("webpack-remove-empty-scripts");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
    mode: 'production',
    entry: {
        jsapplication: './jsapplication.js',
        jsapplicationstyle: './jsapplication.css',
    },
    output: {
        filename: '[name].min.js',
        path: path.resolve(__dirname, './'),
        //assetModuleFilename: 'img/[hash][ext][query]' //default
        assetModuleFilename: '[path][name][ext]' //prevent asset renaming
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, "css-loader"],
            },
        ],

    },
    optimization: {
        minimizer: [
            new CssMinimizerPlugin(),
            '...'
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].min.css",
            runtime: false,
        }),
        new FixStyleOnlyEntriesPlugin()
    ],
};
