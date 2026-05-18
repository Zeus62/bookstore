from Book_Store.reviews import reviews_bp
from Book_Store.models import Review
from Book_Store import db
from flask import render_template, redirect, url_for, flash
from Book_Store.reviews.forms import ReviewForm
from flask_login import login_required, current_user


@reviews_bp.route('/reviews')
@login_required
def reviews():
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.id.desc()).all()
    return render_template('reviews.html', reviews=user_reviews)

@reviews_bp.route('/add_review/<int:book_id>', methods=['POST'])
@login_required
def add_review(book_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            book_id=book_id,
            rating=form.rating.data,
            content=form.content.data.strip(),
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added!', 'success')
    else:
        flash('Failed to add review. Make sure you entered valid data.', 'danger')
    return redirect(url_for('main.book_detail', book_id=book_id))


@reviews_bp.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews.', 'danger')
        return redirect(url_for('reviews_bp.reviews'))

    form = ReviewForm()
    if form.validate_on_submit():
        review.rating = form.rating.data
        review.content = form.content.data.strip()
        db.session.commit()
        flash('Review updated!', 'success')
        return redirect(url_for('reviews_bp.reviews'))

    elif request.method == 'GET':
        form.rating.data = review.rating
        form.content.data = review.content
    return render_template('edit_review.html', form=form, review=review)


@reviews_bp.route('/reviews/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash('You are not allowed to delete this review.', 'danger')
        return redirect(url_for('reviews_bp.reviews'))

    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'info')
    return redirect(url_for('reviews_bp.reviews'))
