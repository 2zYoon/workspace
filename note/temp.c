static int zswap_frontswap_store(unsigned type, pgoff_t offset,
				struct page *page)
{
	struct zswap_tree *tree = zswap_trees[type];
	struct zswap_entry *entry, *dupentry;
	struct crypto_comp *tfm;
	int ret;
	unsigned int hlen, dlen = PAGE_SIZE;
	unsigned long handle, value;
	char *buf;
	u8 *src, *dst;
	struct zswap_header zhdr = { .swpentry = swp_entry(type, offset) };
	gfp_t gfp;

	/* THP isn't supported */
	if (PageTransHuge(page)) {
		ret = -EINVAL;
		goto reject;
	}

	if (!zswap_enabled || !tree) {
		ret = -ENODEV;
		goto reject;
	}

	/* reclaim space if needed */
	if (zswap_is_full()) {
		zswap_pool_limit_hit++;
		if (zswap_shrink()) {
			zswap_reject_reclaim_fail++;
			ret = -ENOMEM;
			goto reject;
		}

		/* A second zswap_is_full() check after
		 * zswap_shrink() to make sure it's now
		 * under the max_pool_percent
		 */
		if (zswap_is_full()) {
			ret = -ENOMEM;
			goto reject;
		}
	}

	/* allocate entry */
	entry = zswap_entry_cache_alloc(GFP_KERNEL);
	if (!entry) {
		zswap_reject_kmemcache_fail++;
		ret = -ENOMEM;
		goto reject;
	}

	if (zswap_same_filled_pages_enabled) {
		src = kmap_atomic(page);
		if (zswap_is_page_same_filled(src, &value)) {
			kunmap_atomic(src);
			entry->offset = offset;
			entry->length = 0;
			entry->value = value;
			atomic_inc(&zswap_same_filled_pages);
			goto insert_entry;
		}
		kunmap_atomic(src);
	}

	/* if entry is successfully added, it keeps the reference */
	entry->pool = zswap_pool_current_get();
	if (!entry->pool) {
		ret = -EINVAL;
		goto freepage;
	}

	/* compress */
	dst = get_cpu_var(zswap_dstmem);
	tfm = *get_cpu_ptr(entry->pool->tfm);
	src = kmap_atomic(page);
	ret = crypto_comp_compress(tfm, src, PAGE_SIZE, dst, &dlen);
	kunmap_atomic(src);
	put_cpu_ptr(entry->pool->tfm);
	if (ret) {
		ret = -EINVAL;
		goto put_dstmem;
	}

	/* store */
	hlen = zpool_evictable(entry->pool->zpool) ? sizeof(zhdr) : 0;
	gfp = __GFP_NORETRY | __GFP_NOWARN | __GFP_KSWAPD_RECLAIM;
	if (zpool_malloc_support_movable(entry->pool->zpool))
		gfp |= __GFP_HIGHMEM | __GFP_MOVABLE;
	ret = zpool_malloc(entry->pool->zpool, hlen + dlen, gfp, &handle);
	if (ret == -ENOSPC) {
		zswap_reject_compress_poor++;
		goto put_dstmem;
	}
	if (ret) {
		zswap_reject_alloc_fail++;
		goto put_dstmem;
	}
	buf = zpool_map_handle(entry->pool->zpool, handle, ZPOOL_MM_RW);
	memcpy(buf, &zhdr, hlen);
	memcpy(buf + hlen, dst, dlen);
	zpool_unmap_handle(entry->pool->zpool, handle);
	put_cpu_var(zswap_dstmem);

	/* populate entry */
	entry->offset = offset;
	entry->handle = handle;
	entry->length = dlen;

insert_entry:
	/* map */
	spin_lock(&tree->lock);
	do {
		ret = zswap_rb_insert(&tree->rbroot, entry, &dupentry);
		if (ret == -EEXIST) {
			zswap_duplicate_entry++;
			/* remove from rbtree */
		    zswap_rb_erase(&tree->rbroot, dupentry);
			zswap_entry_put(tree, dupentry);
		}
	} while (ret == -EEXIST);
	spin_unlock(&tree->lock);

	/* update stats */
	atomic_inc(&zswap_stored_pages);
	zswap_update_total_size();

	return 0;

put_dstmem:
	put_cpu_var(zswap_dstmem);
	zswap_pool_put(entry->pool);
freepage:
	zswap_entry_cache_free(entry);
reject:
	return ret;
}