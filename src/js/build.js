const gulp = require('gulp');
const babel = require('gulp-babel');
 
function buildFunc(done){
  console.log("Building");
  gulp.src('./app.js')
      .pipe(babel({
          presets: ['@babel/env']
      }))
      .pipe(gulp.dest('../builder/static/builder/dist'))
      .on('end', function () {
          if (done) { 
            done(); // callback to signal end of build
          }
      });
};

// run our custom build
buildFunc(function () {
    console.log('Done!');
});
