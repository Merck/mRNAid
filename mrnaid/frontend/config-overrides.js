/* eslint-disable @typescript-eslint/no-var-requires */

const webpack = require('webpack')

module.exports = function override(config) {
  config.resolve.fallback = {
    assert: require.resolve('assert/'),
    buffer: require.resolve('buffer/'),
    stream: require.resolve('stream-browserify'),
    util: require.resolve('util/'),
    zlib: require.resolve('browserify-zlib'),
  }

  config.plugins.push(
    new webpack.ProvidePlugin({
      process: 'process/browser',
      Buffer: ['buffer', 'Buffer'],
    }),
  )

  config.ignoreWarnings = [/Failed to parse source map/]

  return config
}
