const WorkboxPlugin = require('workbox-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const TerserPlugin = require("terser-webpack-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const path = require('path');
// https://github.com/rschristian/babel-plugin-webpack-chunk-name-comments/blob/master/index.js


module.exports = (env, argv) => {
    return {
        // devtool: "inline-source-map",
        devtool: "source-map",
        entry: ["./lino_react/react/index.js"],
        output: {
          filename: (pathData, assetInfo) => {
              return pathData.chunk.name === "main" ? "[name].[contenthash].js" : "main.[name].[contenthash].js"
          },
          chunkFilename: (pathData, assetInfo) => {
              return "main.[name].[chunkhash].js";
          },
          path: path.resolve(__dirname, './lino_react/react/static/react'),
          clean: argv.mode === 'production',
        },
        optimization: {
            minimize: argv.mode === 'production',
            minimizer: [
                new CssMinimizerPlugin(),
                new TerserPlugin({
                    parallel: true,
                    terserOptions: {
                        compress: {
                            ecma: 2015,
                        },
                    },
                }),
            ],
            runtimeChunk: 'single',
            splitChunks: {
                cacheGroups: {
                    utils: {
                        test: /[\\/]node_modules[\\/](weak-key|classnames|query-string|whatwg-fetch|reconnecting-websocket|abort-controller)[\\/]/,
                        name: "tpdep",
                        chunks: "all"
                    },
                    quill: {
                        test: /[\\/]node_modules[\\/]quill[\\/]/,
                        name: "quill",
                        chunks: "all"
                    },
                    // prStyles: {
                    //     test: /[\\/]node_modules[\\/]primereact.*\.css$/,
                    //     name: "prStyles",
                    //     chunks: "all"
                    // },
                    // styles: {
                    //     test: /\.css$/,
                    //     name: "styles",
                    //     chunks: "all"
                    // },
                    prAppRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](toast|button)[\\/]/,
                        name: "prAppRequire",
                        chunks: "all"
                    },
                    prSiteContextRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](progressspinner|progressbar|scrollpanel|overlaypanel|card|dialog|splitbutton)[\\/]/,
                        name: "prSiteContextRequire",
                        chunks: "all"
                    },
                    prLinoBodyRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](selectbutton|dataview|galleria|dropdown|togglebutton)[\\/]/,
                        name: "prLinoBodyRequire",
                        chunks: "all"
                    },
                    prLinoBodyRequireChunk2: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](column|tristatecheckbox|datatable|inputnumber|inputtext|multiselect)[\\/]/,
                        name: "prLinoBodyRequireChunk2",
                        chunks: "all"
                    },
                    prLinoComponentsRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](fileupload|tabview|panel|checkbox|fieldset|password|autocomplete|calendar|editor|splitter|inputswitch)[\\/]/,
                        name: "prLinoComponentsRequire",
                        chunks: "all"
                    },
                }
            }
        },
        module: {
            rules: [{oneOf: [
                {test: [/\.tsx?$/, /\.ts?$/],
                    use: 'ts-loader',
                    exclude: [/node_modules/, /electron/]},
                {test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
                    loader: require.resolve('url-loader'),
                    options: {
                        limit: 10000,
                        name: '/static/media/[name].[hash:8].[ext]',
                        outputPath: '../../'}},
                {test: /\.(woff|woff2|eot|ttf|otf)/i,
                    type: "asset/resource"},
                {test: /\.(js|jsx|mjs)$/,
                    loader: require.resolve('babel-loader'),
                    options: {cacheDirectory: true}},
                {test: /\.css$/,
                    use: [
                        require.resolve('style-loader'),
                        {loader: require.resolve('css-loader'),
                            options: {importLoaders: 1}}]},
                {exclude: [/\.(js|jsx|ts|tsx|mjs|cjs)$/, /\.html$/, /\.json$/],
                    loader: require.resolve('file-loader'),
                    options: {
                        name: '/static/media/[name].[hash:8].[ext]',
                        outputPath: '../../'}},
            ]}]
        },
        plugins: [
            new WorkboxPlugin.InjectManifest({
                swDest: process.cwd() + '/lino_react/react/config/react/service-worker.js',
                swSrc: process.cwd() + '/lino_react/react/components/custom-service-worker.js',
                include: ['/static/react/main.js'],
                exclude: ['/main.js'],
                maximumFileSizeToCacheInBytes: 5000000
            }),
            new HtmlWebpackPlugin({
                filename: "./../../config/react/main.html",
                inject: false,
                minify: false,
                template: "./lino_react/react/components/index.html",
                templateParameters: (htmlWebpackPlugin, assetInfo, tags, options) => {
                    let injects = "";
                    assetInfo.js.forEach((script) => {
                        injects += `<script defer src="{{site.build_static_url('react/${script.split("/").slice(-1)[0]}')}}"></script>\n`
                    });
                    return {
                        webpack_comment: `<!--
        ATTENTION: This content is put here by webpack
        DO NOT MODIFY!
        Edit (lino_react/react/components/index.html) instead
        and run "npm run build".\n-->`,
                        webpack_injects: injects
                    }
                }
            })
        ],
        resolve: {
            alias: {
                'react-dom$': 'react-dom/profiling',
                'scheduler/tracing': 'scheduler/tracing-profiling',
            },
            extensions: [
                '.tsx', '.js', '.json', '.html', '.ts', '.jsx', '.css', '.mjs',
                '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.woff', '.woff2', '.eot',
                '.ttf', '.otf'
            ]
        }
    };
}
