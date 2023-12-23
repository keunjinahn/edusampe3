module.exports = {
  presets: [
    ['@babel/preset-env',
    {
      useBuiltIns: 'entry',
      targets: {
        browsers: [
          "> 1%",
          "last 5 versions",
          "not ie <= 10"
        ]
      }
    }]
    //'@vue/cli-plugin-babel/preset'
    // [
    //   '@vue/app',
    //   {
    //     "useBuiltIns": "entry"
    //   }
    // ]
  ],
  plugins: [
    [
      '@babel/plugin-proposal-decorators',
      {legacy: true}
    ],
    '@babel/plugin-proposal-class-properties',
    '@babel/plugin-transform-runtime',
    '@babel/plugin-transform-classes',
    '@babel/plugin-syntax-dynamic-import',
    '@babel/plugin-proposal-json-strings',
    '@babel/plugin-proposal-function-sent',
    '@babel/plugin-proposal-export-namespace-from',
    '@babel/plugin-proposal-throw-expressions',
    '@babel/plugin-proposal-export-default-from'
  ]
}