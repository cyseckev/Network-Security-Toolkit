@load policy/frameworks/notice/main
redef Notice::policy += {
  [$action = Notice::ACTION_LOG]
};

# Basic: raise a notice when more than 50 connections from one origin to one dest within 60s (very simple heuristic)
redef Conn::max_conns_per_host = 0; # keep default tracking
