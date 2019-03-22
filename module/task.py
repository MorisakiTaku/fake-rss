# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        task
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/4
# ------------------------------------------------------------------------------


def start_task(t_client, d_service, task, logger):
    """任务主模块"""
    entries = task.parse_rss()
    num = 0  # 满足条件的条目数
    for i, entry in enumerate(entries):
        # 判断条目是否满足条件。若满足，则使用transmission api添加任务
        if task.filtrate(entry):
            t_client.add_torrent(entry.get_download_url(), downloader=d_service, download_dir=task.path)
            logger.info("Download \"{}\"".format(entry.title))
            num += 1
    if num:
        logger.info('Finished {} entry(s)'.format(num))
        task.set_time(entries[0].published_timestamp)
    else:
        logger.info("Entry not updated")
