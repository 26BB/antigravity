"""Dashboard views — all protected by @login_required."""

import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger(__name__)


@login_required
def home(request):
    """Main dashboard page. Only accessible to authenticated users."""
    return render(request, 'dashboard/home.html')
