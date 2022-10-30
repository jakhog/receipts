import type { Configuration } from 'webpack';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import ReactRefreshWebpackPlugin from '@pmmmwh/react-refresh-webpack-plugin';
import ReactRefreshTypescript from 'react-refresh-typescript';
import path from 'path';
import TerserWebpackPlugin from 'terser-webpack-plugin';

const config: Configuration = {
    entry: './index.tsx',
    output: {
        path: path.join(__dirname, 'wwwroot'),
        filename: '[name].[chunkhash].bundle.js',
        chunkFilename: '[name].[chunkhash].chunk.js',
    },
    optimization: {
        runtimeChunk: 'single',
        minimize: true,
        minimizer: [
            new TerserWebpackPlugin({
                extractComments: false,
            }),
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js' ],
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                exclude: /node_modules/,
                use: {
                    loader: 'ts-loader',
                    options: {
                        getCustomTransformers: () => ({
                            before: [ ReactRefreshTypescript() ],
                        }),
                        transpileOnly: true,
                    }
                },
            },
            {
                test: /\.css$/,
                use: [ 'style-loader', 'css-loader' ],
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            templateContent: `
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>Receipts</title>
                    </head>
                    <body>
                        <div id="root" />
                    </body>
                </html>
            `,
        }),
        new ReactRefreshWebpackPlugin(),
    ],
};

export default config;