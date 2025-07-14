package evalpro

import rego.v1

default allow_upload_submission := false
default ip_in_allowed_ip_ranges := false
default within_allowed_lab_timeframe := false

allow_upload_submission if {
    input.subject.authenticated
    input.subject.role == "student"
    input.course.published
    not input.course.in_trash
    within_allowed_lab_timeframe
    input.lab.visible
    not input.lab.in_trash
    input.program.visible
    not input.program.in_trash
    ip_in_allowed_ip_ranges
}

allow_upload_submission if {
    input.subject.authenticated
    input.subject.role == "instructor"
    input.subject.mode == "STUDENT"
    input.course.published
    not input.course.in_trash
    within_allowed_lab_timeframe
    input.lab.visible
    not input.lab.in_trash
    input.program.visible
    not input.program.in_trash
    ip_in_allowed_ip_ranges
}

allow_upload_submission if {
    input.subject.authenticated
    input.subject.role == "instructor"
    input.subject.mode == "TEST_DRIVE"
    not input.course.in_trash
    not input.lab.in_trash
    not input.program.in_trash
}

ip_in_allowed_ip_ranges if {
    some range

    range = input.lab.allowed_ip_ranges[_]
    start_ip := ip_to_number(range[0])
    end_ip := ip_to_number(range[1])
    machine_ip := ip_to_number(input.subject.ip_address)

    machine_ip >= start_ip
    machine_ip <= end_ip
}

ip_to_number(ip) = num if {
    octets := split(ip, ".")
    num := to_number(octets[0]) * 256 * 256 * 256 + to_number(octets[1]) * 256 * 256 + to_number(octets[2]) * 256 + to_number(octets[3])
}

within_allowed_lab_timeframe if {
    now := time.now_ns()
    start := time.parse_rfc3339_ns(input.lab.start)
    end := time.parse_rfc3339_ns(input.lab.end)

    start <= now
    now <= end
}
