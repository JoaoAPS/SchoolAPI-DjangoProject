from django.shortcuts import reverse


STUDENT_LIST_URL = reverse('member:student-list')


def student_detail_url(student_id):
    return reverse('member:student-detail', args=[student_id])
