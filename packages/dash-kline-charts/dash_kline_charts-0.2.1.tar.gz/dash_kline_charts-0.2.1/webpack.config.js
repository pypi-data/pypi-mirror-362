const path = require('path');
const packagejson = require('./package.json');

const dashLibraryName = packagejson.name.replace(/-/g, '_');

module.exports = (env, argv) => {
    let mode;

    const overrides = module.exports || {};

    // if user specified mode flag take that value
    if (argv && argv.mode) {
        mode = argv.mode;
    }

    // else if configuration object is already set (module.exports) use that value
    else if (overrides.mode) {
        mode = overrides.mode;
    }

    // else take webpack default (production)
    else {
        mode = 'production';
    }

    let filename = (overrides.output || {}).filename;
    if (!filename) {
        const modeSuffix = mode === 'development' ? 'dev' : 'min';
        filename = `${dashLibraryName}.${modeSuffix}.js`;
    }

    const entry = overrides.entry || { main: './src/lib/index.js' };

    const devtool = overrides.devtool || 'source-map';

    const externals = ('externals' in overrides) ? overrides.externals : ({
        react: 'React',
        'react-dom': 'ReactDOM',
        'plotly.js': 'Plotly'
        // Note: klinecharts is NOT in externals so it gets bundled
    });

    return {
        mode,
        entry,
        output: {
            path: path.resolve(__dirname, dashLibraryName),
            chunkFilename: '[name].js',
            filename,
            library: dashLibraryName,
            libraryTarget: 'window',
        },
        devtool,
        externals,
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'babel-loader',
                        },
                        {
                            loader: 'ts-loader',
                            options: {
                                transpileOnly: true,
                            },
                        },
                    ],
                },
                {
                    test: /\.jsx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                    },
                },
                {
                    test: /\.css$/,
                    use: [
                        {
                            loader: 'style-loader',
                        },
                        {
                            loader: 'css-loader',
                        },
                    ],
                },
            ],
        },
        resolve: {
            extensions: ['.ts', '.tsx', '.js', '.jsx']
        },
        // 添加插件来复制klinecharts文件
        plugins: [
            {
                apply: (compiler) => {
                    compiler.hooks.afterEmit.tap('CopyKlinechartsPlugin', () => {
                        const fs = require('fs');
                        const srcPath = path.resolve(__dirname, 'node_modules/klinecharts/dist/umd/klinecharts.min.js');
                        const destPath = path.resolve(__dirname, dashLibraryName, 'klinecharts.min.js');

                        try {
                            fs.copyFileSync(srcPath, destPath);
                            console.log('✓ klinecharts.min.js copied successfully');
                        } catch (error) {
                            console.error('✗ Failed to copy klinecharts.min.js:', error);
                        }
                    });
                }
            }
        ]
    };
};