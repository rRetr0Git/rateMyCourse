var gulp = require('gulp');

var htmlImport = require('gulp-html-import');

gulp.task('default', function() {
});

gulp.task('importIndexNavbar', function () {
    gulp.src('../../../templates/rateMyCourse/templates/index.html')
        .pipe(htmlImport('../../../templates/rateMyCourse/components/'))
        .pipe(gulp.dest('../../../templates/rateMyCourse'))
})

gulp.task('importCommonNavbar', function () {
    gulp.src('../../../templates/rateMyCourse/templates/searchResult.html')
        .pipe(htmlImport('../../../templates/rateMyCourse/components/'))
        .pipe(gulp.dest('../../../templates/rateMyCourse'))

    gulp.src('../../../templates/rateMyCourse/templates/coursePage.html')
        .pipe(htmlImport('../../../templates/rateMyCourse/components/'))
        .pipe(gulp.dest('../../../templates/rateMyCourse'))

    gulp.src('../../../templates/rateMyCourse/templates/ratePage.html')
        .pipe(htmlImport('../../../templates/rateMyCourse/components/'))
        .pipe(gulp.dest('../../../templates/rateMyCourse'))
})
