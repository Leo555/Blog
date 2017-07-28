var path = require('path');
var webpack = require('webpack');
var autoprefixer = require('autoprefixer');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var CleanPlugin = require('clean-webpack-plugin');

// 模板压缩
// 详见：https://github.com/kangax/html-minifier#options-quick-reference
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
      loader: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [{
          loader: "css-loader",
          options: {
            sourceMap: false,
            modules: false,
            importLoaders: true
          }
        }, {
          loader: "postcss-loader",
          options: {
            plugins: function () {
              return [
                require('autoprefixer')('last 3 versions', 'ie 11')
              ]
            },
            sourceMap: false
          }
        }, {
          loader: "sass-loader",
          options: {
            sourceMap: false
          }
        }]
      })
    }, {
      test: /\.(gif|jpg|png)\??.*$/,
      loader: 'url-loader?limit=500&name=img/[name].[ext]'
    }, {
      test: /\.(woff|svg|eot|ttf)\??.*$/,
      loader: 'file-loader?name=fonts/[name].[hash:6].[ext]'
    }]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.common.js'
    }
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
    new ExtractTextPlugin('[name].[chunkhash:6].css'),
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
    })
  ]
}
