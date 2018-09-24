var path = require('path');
var webpack = require('webpack');
var autoprefixer = require('autoprefixer');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var CleanPlugin = require('clean-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const safeParser = require('postcss-safe-parser');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

var minifyHTML = {
  collapseInlineTagWhitespace: true,
  collapseWhitespace: true,
  minifyJS: true
}

module.exports = {
  watch: true,
  entry: {
    main: './source-src/css/main.scss',
    slider: './source-src/js/slider.js',
    mobile: ['babel-polyfill', './source-src/js/mobile.js']
  },
  output: {
    path: path.resolve(__dirname, './source'),
    publicPath: './',
    filename: '[name].[chunkhash:6].js'
  },
  module: {
    rules: [{
      test: /\.js$/,
      loader: 'babel-loader?cacheDirectory',
      exclude: /node_modules/
    }, {
      test: /\.html$/,
      loader: 'html'
    }, {
      test: /\.(scss|sass|css)$/,
      loader: [MiniCssExtractPlugin.loader, {
        loader: "css-loader",
        options: {
          sourceMap: false,
          modules: false,
          importLoaders: true
        }
      }, {
        loader: require.resolve('postcss-loader'),
        options: {
          ident: 'postcss',
          plugins: () => [
            require('postcss-flexbugs-fixes'),
            autoprefixer({
              flexbox: 'no-2009',
            }),
          ],
          sourceMap: false,
        },
      }, {
        loader: "sass-loader",
        options: {
          sourceMap: false
        }
      }]
    }, {
      test: /\.(gif|jpg|png)\??.*$/,
      loader: 'url-loader?limit=500&name=img/[name].[ext]'
    }, {
      test: /\.(woff|svg|eot|ttf)\??.*$/,
      loader: 'file-loader?name=fonts/[name].[ext]'
    }]
  },
  optimization: {
    minimizer: [
      new UglifyJsPlugin(),
      new OptimizeCSSAssetsPlugin({
        cssProcessorOptions: {
          parser: safeParser,
          discardComments: {
            removeAll: true
          }
        }
      }),
    ]
  },
  plugins: [
    new CleanPlugin('source'),
    new webpack.LoaderOptionsPlugin({
      minimize: true,
      options: {
        postcss: [require('autoprefixer')({
          browsers: ['last 3 version']
        })]
      }
    }),
    new HtmlWebpackPlugin({
      inject: false,
      cache: false,
      minify: minifyHTML,
      template: './source-src/script.ejs',
      filename: '../layout/_partial/script.ejs'
    }),
    new HtmlWebpackPlugin({
      inject: false,
      cache: false,
      minify: minifyHTML,
      template: './source-src/css.ejs',
      filename: '../layout/_partial/css.ejs'
    }),
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash:8].css',
      chunkFilename: '[name].[contenthash:8].chunk.css',
    }),
  ]
}
