from Book_Store.reviews import reviews_bp
from Book_Store.models import Review
from Book_Store import db
from flask import render_template, redirect, url_for, flash
from Book_Store.reviews.forms import ReviewForm
from flask_login import login_required, current_user


@reviews_bp.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            title=form.title.data.strip(),
            content=form.content.data.strip(),
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added!', 'success')
        return redirect(url_for('reviews_bp.reviews'))

    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.id.desc()).all()
    return render_template('reviews.html', form=form, reviews=user_reviews)


@reviews_bp.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews.', 'danger')
        return redirect(url_for('reviews_bp.reviews'))

    form = ReviewForm()
    if form.validate_on_submit():
        review.title = form.title.data.strip()
        review.content = form.content.data.strip()
        db.session.commit()
        flash('Review updated!', 'success')
        return redirect(url_for('reviews_bp.reviews'))

    form.title.data = review.title
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
